/**
 * API Client - Helper functions for API requests
 */

/**
 * Base API URL
 */
const API_BASE_URL = '/api';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, finalOptions);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * GET request
 */
async function get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    
    return fetchAPI(url, {
        method: 'GET',
    });
}

/**
 * POST request
 */
async function post(endpoint, data = {}) {
    return fetchAPI(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

/**
 * PUT request
 */
async function put(endpoint, data = {}) {
    return fetchAPI(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
}

/**
 * DELETE request
 */
async function del(endpoint) {
    return fetchAPI(endpoint, {
        method: 'DELETE',
    });
}

/**
 * File upload request
 */
async function uploadFile(endpoint, file, additionalData = {}) {
    const formData = new FormData();
    formData.append('file', file);
    
    Object.keys(additionalData).forEach(key => {
        formData.append(key, additionalData[key]);
    });
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            body: formData,
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        return data;
    } catch (error) {
        console.error('Upload Error:', error);
        throw error;
    }
}

/**
 * Projects API
 */
const ProjectsAPI = {
    async list(category = null) {
        const params = category ? { category } : {};
        return get('/projects', params);
    },
    
    async get(id) {
        return get(`/projects/${id}`);
    },
    
    async create(data) {
        return post('/projects', data);
    },
    
    async update(id, data) {
        return put(`/projects/${id}`, data);
    },
    
    async delete(id) {
        return del(`/projects/${id}`);
    }
};

/**
 * Services API
 */
const ServicesAPI = {
    async list() {
        return get('/services');
    },
    
    async get(id) {
        return get(`/services/${id}`);
    },
    
    async create(data) {
        return post('/services', data);
    },
    
    async update(id, data) {
        return put(`/services/${id}`, data);
    },
    
    async delete(id) {
        return del(`/services/${id}`);
    }
};

/**
 * Testimonials API
 */
const TestimonialsAPI = {
    async list() {
        return get('/testimonials');
    },
    
    async get(id) {
        return get(`/testimonials/${id}`);
    },
    
    async create(data) {
        return post('/testimonials', data);
    },
    
    async update(id, data) {
        return put(`/testimonials/${id}`, data);
    },
    
    async delete(id) {
        return del(`/testimonials/${id}`);
    }
};

/**
 * Images API
 */
const ImagesAPI = {
    async upload(file, relatedTo = 'general', relatedId = null) {
        return uploadFile('/images', file, { related_to: relatedTo, related_id: relatedId });
    },
    
    async delete(id) {
        return del(`/images/${id}`);
    },
    
    async list() {
        return get('/images');
    }
};

/**
 * Contact API
 */
const ContactAPI = {
    async submit(data) {
        return post('/contact', data);
    }
};

/**
 * Loading indicator helper
 */
function showLoading(element) {
    element.classList.add('loading');
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.id = 'loading-spinner';
    element.appendChild(spinner);
}

function hideLoading(element) {
    element.classList.remove('loading');
    const spinner = element.querySelector('#loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

/**
 * Error display helper
 */
function showError(message, container = null) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'flash-message flash-error';
    errorDiv.textContent = message;
    
    if (container) {
        container.appendChild(errorDiv);
    } else {
        document.body.appendChild(errorDiv);
    }
    
    TCDAnimations.slideUp(errorDiv);
    
    setTimeout(() => {
        errorDiv.style.opacity = '0';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

/**
 * Success display helper
 */
function showSuccess(message, container = null) {
    const successDiv = document.createElement('div');
    successDiv.className = 'flash-message flash-success';
    successDiv.textContent = message;
    
    if (container) {
        container.appendChild(successDiv);
    } else {
        document.body.appendChild(successDiv);
    }
    
    TCDAnimations.slideUp(successDiv);
    
    setTimeout(() => {
        successDiv.style.opacity = '0';
        setTimeout(() => successDiv.remove(), 300);
    }, 5000);
}

// Export API client
window.TCDAPI = {
    fetchAPI,
    get,
    post,
    put,
    delete: del,
    uploadFile,
    ProjectsAPI,
    ServicesAPI,
    TestimonialsAPI,
    ImagesAPI,
    ContactAPI,
    showLoading,
    hideLoading,
    showError,
    showSuccess
};
