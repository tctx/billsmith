/**
 * BillSmith Frontend Application
 * 
 * Main JavaScript module handling API communication and UI interactions.
 */

class BillSmithApp {
    constructor() {
        this.apiBase = '/api/v1';
        this.currentCategory = null;
        this.categories = [];
        this.bills = [];
        
        this.init();
    }

    async init() {
        await this.loadCategories();
        this.setupEventListeners();
        this.setupChart();
        
        // Select first category by default
        if (this.categories.length > 0) {
            this.selectCategory(this.categories[0]);
        }
    }

    // ===== API METHODS =====

    async fetchAPI(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            this.showToast(`Error: ${error.message}`, 'error');
            throw error;
        }
    }

    async loadCategories() {
        try {
            this.categories = await this.fetchAPI('/categories');
            this.renderCategories();
        } catch (error) {
            console.error('Failed to load categories:', error);
        }
    }

    async loadDashboardData(categoryId) {
        try {
            const data = await this.fetchAPI(`/analytics/dashboard/${categoryId}`);
            this.renderDashboard(data);
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        }
    }

    async loadBills(categoryId = null) {
        try {
            const query = categoryId ? `?category_id=${categoryId}` : '';
            this.bills = await this.fetchAPI(`/bills${query}`);
            this.renderDocuments(this.bills);
        } catch (error) {
            console.error('Failed to load bills:', error);
        }
    }

    async createMockBill() {
        try {
            const vendors = ['Electric Company', 'Water Works', 'Gas & Power', 'Internet Plus'];
            const vendor = vendors[Math.floor(Math.random() * vendors.length)];
            const amount = Math.floor(Math.random() * 200) + 50;
            
            const bill = await this.fetchAPI('/bills/mock', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    vendor,
                    amount,
                    category_name: this.currentCategory?.name || 'Electricity'
                })
            });
            
            this.showToast(`Created mock bill: ${vendor} - $${amount}`, 'success');
            
            // Refresh data
            if (this.currentCategory) {
                await this.loadDashboardData(this.currentCategory.id);
            }
            
        } catch (error) {
            console.error('Failed to create mock bill:', error);
        }
    }

    // ===== UI RENDERING =====

    renderCategories() {
        const list = document.getElementById('categoriesList');
        list.innerHTML = '';

        this.categories.forEach(category => {
            const item = document.createElement('li');
            item.className = 'sidebar__item';
            item.innerHTML = `
                <span class="swatch" style="background: ${category.color_hex}"></span>
                <span class="label">${category.name}</span>
            `;
            
            item.addEventListener('click', () => this.selectCategory(category));
            list.appendChild(item);
        });
    }

    async selectCategory(category) {
        // Update active state
        document.querySelectorAll('.sidebar__item').forEach(item => {
            item.classList.remove('sidebar__item--active');
        });
        
        event?.target.closest('.sidebar__item')?.classList.add('sidebar__item--active');
        
        this.currentCategory = category;
        
        // Update hero card
        document.getElementById('heroTitle').textContent = category.name;
        document.getElementById('heroSubtitle').textContent = `Manage your ${category.name.toLowerCase()} payments and documents`;
        
        // Load dashboard data
        await this.loadDashboardData(category.id);
    }

    renderDashboard(data) {
        if (data.error) {
            this.showToast(data.error, 'error');
            return;
        }

        const { summary, payment_trends, important_documents } = data;

        // Update summary cards
        if (summary.last_payment) {
            document.getElementById('lastPaymentAmount').textContent = 
                `$${summary.last_payment.amount.toFixed(2)}`;
            document.getElementById('lastPaymentDate').textContent = 
                new Date(summary.last_payment.date).toLocaleDateString();
        } else {
            document.getElementById('lastPaymentAmount').textContent = '-';
            document.getElementById('lastPaymentDate').textContent = 'No payments yet';
        }

        document.getElementById('nextDueDate').textContent = 
            summary.next_due ? new Date(summary.next_due).toLocaleDateString() : '-';
        
        document.getElementById('yearToDateAmount').textContent = 
            `$${summary.year_to_date.toFixed(2)}`;

        // Update chart
        this.updateChart(payment_trends, data.category.color_hex);

        // Update documents table
        this.renderDocuments(important_documents);
    }

    renderDocuments(documents) {
        const tbody = document.getElementById('documentsTableBody');
        tbody.innerHTML = '';

        if (!documents || documents.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center">
                        No documents found. <button class="btn btn--secondary" onclick="app.createMockBill()">Add Sample Bill</button>
                    </td>
                </tr>
            `;
            return;
        }

        documents.forEach(doc => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${doc.title || `${doc.vendor} - ${doc.invoice_number || 'Invoice'}`}</td>
                <td>${new Date(doc.date || doc.created_at).toLocaleDateString()}</td>
                <td>$${doc.amount.toFixed(2)}</td>
                <td>
                    ${doc.needs_review ? 
                        '<span class="badge badge--needs-review">Needs Review</span>' : 
                        '<span class="badge badge--category">Processed</span>'
                    }
                </td>
                <td>
                    <button class="btn btn--secondary" onclick="app.viewBill(${doc.id})">View</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    // ===== CHART RENDERING =====

    setupChart() {
        this.chartSvg = d3.select('#trendsChart');
        this.chartWidth = 800;
        this.chartHeight = 300;
        this.chartMargin = { top: 20, right: 30, bottom: 40, left: 60 };
    }

    updateChart(data, color = '#2222FF') {
        if (!data || data.length === 0) {
            this.chartSvg.selectAll('*').remove();
            this.chartSvg.append('text')
                .attr('x', this.chartWidth / 2)
                .attr('y', this.chartHeight / 2)
                .attr('text-anchor', 'middle')
                .style('fill', '#666')
                .text('No payment data available');
            return;
        }

        // Clear previous chart
        this.chartSvg.selectAll('*').remove();

        // Set up scales
        const xScale = d3.scaleTime()
            .domain(d3.extent(data, d => new Date(d.date)))
            .range([this.chartMargin.left, this.chartWidth - this.chartMargin.right]);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.amount)])
            .nice()
            .range([this.chartHeight - this.chartMargin.bottom, this.chartMargin.top]);

        // Create line generator
        const line = d3.line()
            .x(d => xScale(new Date(d.date)))
            .y(d => yScale(d.amount))
            .curve(d3.curveMonotoneX);

        // Add axes
        this.chartSvg.append('g')
            .attr('transform', `translate(0,${this.chartHeight - this.chartMargin.bottom})`)
            .call(d3.axisBottom(xScale).tickFormat(d3.timeFormat('%b')));

        this.chartSvg.append('g')
            .attr('transform', `translate(${this.chartMargin.left},0)`)
            .call(d3.axisLeft(yScale).tickFormat(d => `$${d}`));

        // Add line
        this.chartSvg.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', color)
            .attr('stroke-width', 2)
            .attr('d', line);

        // Add points
        this.chartSvg.selectAll('.dot')
            .data(data)
            .enter().append('circle')
            .attr('class', 'dot')
            .attr('cx', d => xScale(new Date(d.date)))
            .attr('cy', d => yScale(d.amount))
            .attr('r', 4)
            .attr('fill', color)
            .on('mouseover', (event, d) => {
                this.showTooltip(event, `$${d.amount.toFixed(2)}<br>${new Date(d.date).toLocaleDateString()}`);
            })
            .on('mouseout', () => this.hideTooltip());
    }

    // ===== EVENT HANDLERS =====

    setupEventListeners() {
        // Add Bill button
        document.getElementById('addBillBtn').addEventListener('click', () => {
            this.createMockBill(); // For MVP, create mock bill
        });

        // File upload (future implementation)
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                this.handleFileUpload(e.target.files);
            });
        }
    }

    handleFileUpload(files) {
        // TODO: Implement actual file upload
        console.log('Files selected:', files);
        this.showToast('File upload coming soon!', 'info');
    }

    viewBill(billId) {
        // TODO: Navigate to bill detail view
        console.log('View bill:', billId);
        this.showToast(`Bill detail view coming soon!`, 'info');
    }

    // ===== UTILITY METHODS =====

    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast--${type}`;
        toast.innerHTML = `
            <span>${message}</span>
            <button class="toast__close">&times;</button>
        `;

        container.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.remove();
        }, 5000);

        // Manual close
        toast.querySelector('.toast__close').addEventListener('click', () => {
            toast.remove();
        });
    }

    showTooltip(event, content) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.innerHTML = content;
        tooltip.style.position = 'absolute';
        tooltip.style.left = event.pageX + 10 + 'px';
        tooltip.style.top = event.pageY - 10 + 'px';
        tooltip.style.background = 'rgba(0,0,0,0.8)';
        tooltip.style.color = 'white';
        tooltip.style.padding = '8px';
        tooltip.style.borderRadius = '4px';
        tooltip.style.pointerEvents = 'none';
        tooltip.style.zIndex = '1000';
        
        document.body.appendChild(tooltip);
        this.currentTooltip = tooltip;
    }

    hideTooltip() {
        if (this.currentTooltip) {
            this.currentTooltip.remove();
            this.currentTooltip = null;
        }
    }
}

// ===== CSS FOR TOAST & MODAL =====
const additionalCSS = `
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: var(--z-modal);
}

.modal__content {
    background: white;
    border-radius: var(--card-radius);
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
}

.modal__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-4);
    border-bottom: 1px solid #E0E0E0;
}

.modal__close {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
}

.toast-container {
    position: fixed;
    bottom: 20px;
    left: 20px;
    z-index: var(--z-toast);
}

.toast {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3);
    margin-bottom: var(--space-2);
    background: white;
    border-radius: var(--button-radius);
    box-shadow: var(--shadow-200);
    min-width: 300px;
}

.toast--success { border-left: 4px solid var(--color-success); }
.toast--error { border-left: 4px solid var(--color-error); }
.toast--info { border-left: 4px solid var(--color-accent-default); }

.toast__close {
    background: none;
    border: none;
    cursor: pointer;
    margin-left: auto;
}
`;

// Add additional CSS to the page
const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style);

// Initialize the application
const app = new BillSmithApp();

// Make app globally available for debugging
window.app = app; 