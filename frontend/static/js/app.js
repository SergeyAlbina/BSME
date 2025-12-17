// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';
let authToken = localStorage.getItem('authToken');
let currentUser = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    if (authToken) {
        checkAuth();
    } else {
        showScreen('login');
    }

    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Login form
    document.getElementById('login-form')?.addEventListener('submit', handleLogin);

    // Logout button
    document.getElementById('logout-btn')?.addEventListener('click', handleLogout);

    // Navigation items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const view = item.dataset.view;
            loadView(view);
        });
    });

    // Filters
    document.getElementById('apply-filters')?.addEventListener('click', applyFilters);
    document.getElementById('reset-filters')?.addEventListener('click', resetFilters);

    // Modal close
    document.querySelector('.close')?.addEventListener('click', () => {
        document.getElementById('ticket-modal').style.display = 'none';
    });
}

// Authentication
async function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Неверное имя пользователя или пароль');
        }

        const data = await response.json();
        authToken = data.access_token;
        localStorage.setItem('authToken', authToken);

        await checkAuth();
    } catch (error) {
        showError('login-error', error.message);
    }
}

async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Unauthorized');
        }

        currentUser = await response.json();
        document.getElementById('user-name').textContent = currentUser.full_name;
        showScreen('dashboard');
        loadTickets();
    } catch (error) {
        handleLogout();
    }
}

function handleLogout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    showScreen('login');
}

// UI Functions
function showScreen(screenName) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.style.display = 'none';
    });
    document.getElementById(`${screenName}-screen`).style.display = 'block';
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

// Load Views
function loadView(view) {
    const titles = {
        'tickets': 'Все заявки',
        'my-tickets': 'Мои заявки',
        'assigned': 'Назначенные мне',
        'stats': 'Статистика'
    };

    document.getElementById('content-title').textContent = titles[view] || 'Заявки';

    if (view === 'stats') {
        loadStats();
    } else {
        loadTickets(view);
    }
}

// Load Tickets
async function loadTickets(view = 'tickets') {
    const ticketsList = document.getElementById('tickets-list');
    ticketsList.innerHTML = '<div class="loading">Загрузка...</div>';

    try {
        let url = `${API_BASE_URL}/tickets/`;
        const params = new URLSearchParams();

        if (view === 'my-tickets') {
            params.append('created_by_me', 'true');
        } else if (view === 'assigned') {
            params.append('assigned_to_me', 'true');
        }

        // Apply filters
        const status = document.getElementById('filter-status').value;
        const priority = document.getElementById('filter-priority').value;
        const category = document.getElementById('filter-category').value;

        if (status) params.append('status', status);
        if (priority) params.append('priority', priority);
        if (category) params.append('category', category);

        if (params.toString()) {
            url += '?' + params.toString();
        }

        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load tickets');
        }

        const tickets = await response.json();
        renderTickets(tickets);
    } catch (error) {
        ticketsList.innerHTML = '<div class="error-message">Ошибка загрузки заявок</div>';
    }
}

function renderTickets(tickets) {
    const ticketsList = document.getElementById('tickets-list');

    if (tickets.length === 0) {
        ticketsList.innerHTML = '<div class="loading">Заявок не найдено</div>';
        return;
    }

    ticketsList.innerHTML = tickets.map(ticket => `
        <div class="ticket-card" onclick="showTicketDetail(${ticket.id})">
            <div class="ticket-header">
                <span class="ticket-number">#${ticket.ticket_number}</span>
                <div>
                    <span class="badge badge-status-${ticket.status}">${formatStatus(ticket.status)}</span>
                    <span class="badge badge-priority-${ticket.priority}">${formatPriority(ticket.priority)}</span>
                </div>
            </div>
            <div class="ticket-title">${ticket.title}</div>
            <div class="ticket-meta">
                <span>📂 ${formatCategory(ticket.category)}</span>
                <span>📅 ${formatDate(ticket.created_at)}</span>
            </div>
        </div>
    `).join('');
}

async function showTicketDetail(ticketId) {
    const modal = document.getElementById('ticket-modal');
    const detail = document.getElementById('ticket-detail');

    modal.style.display = 'block';
    detail.innerHTML = '<div class="loading">Загрузка...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/tickets/${ticketId}`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load ticket details');
        }

        const ticket = await response.json();
        renderTicketDetail(ticket);
    } catch (error) {
        detail.innerHTML = '<div class="error-message">Ошибка загрузки деталей заявки</div>';
    }
}

function renderTicketDetail(ticket) {
    const detail = document.getElementById('ticket-detail');

    const commentsHtml = ticket.comments?.map(comment => `
        <div style="border-left: 3px solid #007bff; padding-left: 15px; margin: 10px 0;">
            <strong>Комментарий</strong><br>
            <small>${formatDate(comment.created_at)}</small>
            <p>${comment.comment_text}</p>
        </div>
    `).join('') || '<p>Нет комментариев</p>';

    detail.innerHTML = `
        <h2>#${ticket.ticket_number} - ${ticket.title}</h2>
        <div style="margin: 20px 0;">
            <span class="badge badge-status-${ticket.status}">${formatStatus(ticket.status)}</span>
            <span class="badge badge-priority-${ticket.priority}">${formatPriority(ticket.priority)}</span>
        </div>

        <div style="margin: 20px 0;">
            <strong>Категория:</strong> ${formatCategory(ticket.category)}<br>
            <strong>Создана:</strong> ${formatDate(ticket.created_at)}<br>
            ${ticket.location ? `<strong>Местоположение:</strong> ${ticket.location}<br>` : ''}
            ${ticket.equipment_type ? `<strong>Оборудование:</strong> ${ticket.equipment_type}<br>` : ''}
        </div>

        <div style="margin: 20px 0;">
            <h3>Описание</h3>
            <p>${ticket.description || 'Нет описания'}</p>
        </div>

        <div style="margin: 20px 0;">
            <h3>Комментарии</h3>
            ${commentsHtml}
        </div>

        ${currentUser.role !== 'user' ? `
            <div style="margin-top: 20px;">
                <button class="btn btn-primary" onclick="assignToMe(${ticket.id})">Назначить на себя</button>
                <button class="btn btn-secondary" onclick="changeStatus(${ticket.id})">Изменить статус</button>
            </div>
        ` : ''}
    `;
}

// Filters
function applyFilters() {
    loadTickets();
}

function resetFilters() {
    document.getElementById('filter-status').value = '';
    document.getElementById('filter-priority').value = '';
    document.getElementById('filter-category').value = '';
    loadTickets();
}

// Formatters
function formatStatus(status) {
    const statuses = {
        'new': 'Новая',
        'in_progress': 'В работе',
        'resolved': 'Решена',
        'closed': 'Закрыта'
    };
    return statuses[status] || status;
}

function formatPriority(priority) {
    const priorities = {
        'critical': 'Критический',
        'high': 'Высокий',
        'medium': 'Средний',
        'low': 'Низкий'
    };
    return priorities[priority] || priority;
}

function formatCategory(category) {
    const categories = {
        'hardware': 'Оборудование',
        'software': 'ПО'
    };
    return categories[category] || category;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU');
}

// Actions
async function assignToMe(ticketId) {
    try {
        const response = await fetch(`${API_BASE_URL}/tickets/${ticketId}/assign`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to assign ticket');
        }

        alert('Заявка назначена на вас');
        showTicketDetail(ticketId);
        loadTickets();
    } catch (error) {
        alert('Ошибка назначения заявки');
    }
}

async function changeStatus(ticketId) {
    const newStatus = prompt('Введите новый статус (new, in_progress, resolved, closed):');

    if (!newStatus) return;

    try {
        const response = await fetch(`${API_BASE_URL}/tickets/${ticketId}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });

        if (!response.ok) {
            throw new Error('Failed to update status');
        }

        alert('Статус обновлен');
        showTicketDetail(ticketId);
        loadTickets();
    } catch (error) {
        alert('Ошибка обновления статуса');
    }
}

function loadStats() {
    const ticketsList = document.getElementById('tickets-list');
    ticketsList.innerHTML = `
        <div style="padding: 20px;">
            <h3>Статистика</h3>
            <p>Раздел в разработке...</p>
        </div>
    `;
}
