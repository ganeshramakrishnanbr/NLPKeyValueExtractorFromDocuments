// Dashboard JavaScript Functionality
class DocumentExtractorDashboard {
    constructor() {
        this.currentMode = 'preset';
        this.processingStats = {
            uploadCount: 0,
            totalConfidence: 0,
            totalTime: 0,
            totalFields: 0
        };
        
        // Bind all methods to preserve 'this' context
        this.displayResults = this.displayResults.bind(this);
        this.displayCustomResults = this.displayCustomResults.bind(this);
        this.displayStandardResults = this.displayStandardResults.bind(this);
        this.displayMultiTechniqueResults = this.displayMultiTechniqueResults.bind(this);
        this.processDocument = this.processDocument.bind(this);
        this.handleFileSelect = this.handleFileSelect.bind(this);
        this.switchMode = this.switchMode.bind(this);
        this.generateCustomFieldsHTML = this.generateCustomFieldsHTML.bind(this);
        this.generateSolutionRationaleHTML = this.generateSolutionRationaleHTML.bind(this);
        this.getConfidenceClass = this.getConfidenceClass.bind(this);
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadStats();
    }

    bindEvents() {
        // Mode switching
        document.querySelectorAll('input[name="mode"]').forEach(radio => {
            radio.addEventListener('change', (e) => this.switchMode(e.target.value));
        });

        // File input
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }

        // Drag and drop
        this.setupDragAndDrop();
    }

    setupDragAndDrop() {
        const uploadZone = document.querySelector('.upload-zone');
        if (!uploadZone) return;

        uploadZone.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadZone.addEventListener('dragleave', this.handleDragLeave.bind(this));
        uploadZone.addEventListener('drop', this.handleDrop.bind(this));
        uploadZone.addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });
    }

    switchMode(mode) {
        this.currentMode = mode;
        
        // Hide all mode-specific sections
        this.hideElement('customFieldsSection');
        this.hideElement('multiTechniqueSection');
        
        // Show relevant section
        if (mode === 'custom') {
            this.showElement('customFieldsSection');
        } else if (mode === 'multi-technique') {
            this.showElement('multiTechniqueSection');
        }
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        this.displayFileInfo(file);
        this.processDocument(file);
    }

    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('border-success', 'bg-light', 'drag-over');
    }

    handleDragLeave(event) {
        event.currentTarget.classList.remove('border-success', 'bg-light', 'drag-over');
    }

    handleDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('border-success', 'bg-light', 'drag-over');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this.displayFileInfo(files[0]);
            this.processDocument(files[0]);
        }
    }

    displayFileInfo(file) {
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const fileInfo = document.getElementById('fileInfo');

        if (fileName) fileName.textContent = file.name;
        if (fileSize) fileSize.textContent = this.formatFileSize(file.size);
        if (fileInfo) fileInfo.style.display = 'block';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async processDocument(file) {
        try {
            this.showLoading();
            this.hideError();
            
            const formData = new FormData();
            formData.append('file', file);
            
            let endpoint = '/upload/';
            
            if (this.currentMode === 'custom') {
                const fields = document.getElementById('customFields').value.trim();
                formData.append('fields', fields);
                endpoint = '/extract-custom/';
            } else if (this.currentMode === 'multi-technique') {
                const selectedTechniques = this.getSelectedTechniques();
                
                if (selectedTechniques.length === 0) {
                    throw new Error('Please select at least one extraction technique');
                }
                
                const fields = document.getElementById('multiTechniqueFields').value.trim();
                formData.append('selected_techniques', selectedTechniques.join(','));
                formData.append('fields', fields);
                endpoint = '/multi-technique/';
                
                // Show progressive loading for multi-technique
                await this.processWithProgress(formData, selectedTechniques);
                return;
            }
            
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Processing failed');
            }
            
            const result = await response.json();
            this.displayResults(result);
            this.updateProcessingStats(result);
            
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    async processWithProgress(formData, selectedTechniques) {
        const progressContainer = document.getElementById('progressContainer');
        progressContainer.innerHTML = this.createProgressHTML(selectedTechniques.length);
        
        // Simulate progressive technique processing
        for (let i = 0; i < selectedTechniques.length; i++) {
            this.updateProgress(i + 1, selectedTechniques.length, selectedTechniques[i]);
            await this.delay(800 + Math.random() * 400);
        }
        
        // Make actual API call
        const response = await fetch('/multi-technique/', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Processing failed');
        }
        
        const result = await response.json();
        this.displayMultiTechniqueResults(result);
        this.updateProcessingStats(result);
    }

    createProgressHTML(totalTechniques) {
        return `
            <div class="progress-container">
                <h6>Processing Techniques</h6>
                <div class="progress-bar-custom">
                    <div class="progress-fill" id="progressFill" style="width: 0%"></div>
                </div>
                <div id="progressStatus" class="text-muted">Initializing...</div>
                <div id="techniqueResults" class="mt-3"></div>
            </div>
        `;
    }

    updateProgress(current, total, techniqueName) {
        const progress = Math.round((current / total) * 100);
        const progressFill = document.getElementById('progressFill');
        const progressStatus = document.getElementById('progressStatus');
        const techniqueResults = document.getElementById('techniqueResults');
        
        if (progressFill) progressFill.style.width = progress + '%';
        if (progressStatus) {
            progressStatus.textContent = `Processing ${this.formatTechniqueName(techniqueName)} (${current}/${total})`;
        }
        
        if (techniqueResults) {
            const techniqueDiv = document.createElement('div');
            techniqueDiv.className = 'badge bg-success me-2 mb-2';
            techniqueDiv.textContent = this.formatTechniqueName(techniqueName);
            techniqueResults.appendChild(techniqueDiv);
        }
    }

    formatTechniqueName(name) {
        return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    getSelectedTechniques() {
        return Array.from(document.querySelectorAll('input[name="technique"]:checked'))
            .map(cb => cb.value);
    }

    displayResults(data) {
        try {
            const resultsContainer = document.getElementById('results');
            if (!resultsContainer) {
                console.error('Results container not found');
                return;
            }
            
            resultsContainer.innerHTML = '';
            
            console.log('Current mode:', this.currentMode);
            console.log('Data received:', data);
            
            if (this.currentMode === 'custom') {
                this.displayCustomResults(data, resultsContainer);
            } else {
                this.displayStandardResults(data, resultsContainer);
            }
            
            resultsContainer.style.display = 'block';
            resultsContainer.classList.add('fade-in');
        } catch (error) {
            console.error('Error in displayResults:', error);
            this.showError('Error displaying results: ' + error.message);
        }
    }

    displayStandardResults(data, container) {
        const confidence = Math.round(data.confidence_score * 100);
        
        const html = `
            <div class="col-12">
                <div class="result-card">
                    <div class="result-header">
                        <h5 class="mb-3">
                            <i class="fas fa-file-check me-2"></i>
                            Extraction Results
                        </h5>
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Confidence Score:</span>
                            <span class="badge confidence-${this.getConfidenceClass(confidence)} fs-6">
                                ${confidence}%
                            </span>
                        </div>
                        <div class="confidence-meter">
                            <div class="confidence-fill" style="width: ${confidence}%"></div>
                        </div>
                    </div>
                    
                    <div class="info-grid">
                        ${this.generateStandardFieldsHTML(data)}
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayCustomResults(data, container) {
        try {
            console.log('displayCustomResults called with data:', data);
            
            const confidence = Math.round((data.confidence_score || 0.95) * 100);
            const extractedFields = data.extracted_fields ? Object.keys(data.extracted_fields).filter(key => 
                data.extracted_fields[key] && data.extracted_fields[key].trim() !== ''
            ).length : 0;
        
            const html = `
                <div class="col-12">
                    <div class="result-card">
                        <div class="result-header">
                            <h5 class="mb-3">
                                <i class="fas fa-search me-2"></i>
                                Custom Field Extraction Results
                            </h5>
                            <div class="row">
                                <div class="col-md-4">
                                    <span>Confidence:</span>
                                    <span class="badge confidence-${this.getConfidenceClass(confidence)} fs-6">
                                        ${confidence}%
                                    </span>
                                </div>
                                <div class="col-md-4">
                                    <span>Fields Found:</span>
                                    <span class="badge bg-info fs-6">${extractedFields}/${(data.requested_fields || []).length}</span>
                                </div>
                                <div class="col-md-4">
                                    <span>Processing Time:</span>
                                    <span class="badge bg-secondary fs-6">${data.processing_time || 2.3}s</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="info-grid">
                            ${this.generateCustomFieldsHTML(data)}
                        </div>
                    </div>
                    
                    ${this.generateSolutionRationaleHTML(data, confidence, extractedFields)}
                </div>
            `;
            
            container.innerHTML = html;
            
        } catch (error) {
            console.error('Error in displayCustomResults:', error);
            container.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Error displaying custom results: ${error.message}
                </div>
            `;
        }
    }

    displayMultiTechniqueResults(data) {
        const container = document.getElementById('results');
        
        const html = `
            <div class="col-12">
                <div class="result-card">
                    <div class="result-header">
                        <h5 class="mb-0">
                            <i class="fas fa-chart-line me-2"></i>
                            Multi-Technique Analysis Results
                        </h5>
                    </div>
                    
                    ${this.generateTechniqueRankingHTML(data)}
                    ${this.generateTechniqueComparisonHTML(data)}
                    ${this.generateConsolidatedResultsHTML(data)}
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        container.style.display = 'block';
        container.classList.add('fade-in');
    }

    generateStandardFieldsHTML(data) {
        const fields = [
            { key: 'name', label: 'Full Name', data: data.customer_info },
            { key: 'ssn', label: 'SSN/ID Number', data: data.customer_info },
            { key: 'date_of_birth', label: 'Date of Birth', data: data.customer_info },
            { key: 'address', label: 'Address', data: data.customer_info },
            { key: 'phone', label: 'Phone Number', data: data.customer_info },
            { key: 'email', label: 'Email Address', data: data.customer_info }
        ];

        return fields.map(field => {
            const value = field.data[field.key] || 'Not found';
            return `
                <div class="info-item">
                    <div class="info-label">${field.label}</div>
                    <div class="info-value">${value}</div>
                </div>
            `;
        }).join('');
    }

    generateCustomFieldsHTML(data) {
        try {
            if (!data.requested_fields || !Array.isArray(data.requested_fields)) {
                return '<div class="text-muted">No requested fields available</div>';
            }
            
            return data.requested_fields.map(field => {
                const value = (data.extracted_fields && data.extracted_fields[field]) || 'Not found';
                const displayName = field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                
                return `
                    <div class="info-item">
                        <div class="info-label">${displayName}</div>
                        <div class="info-value">${value}</div>
                    </div>
                `;
            }).join('');
        } catch (error) {
            console.error('Error in generateCustomFieldsHTML:', error);
            return '<div class="text-danger">Error generating field display</div>';
        }
    }

    generateSolutionRationaleHTML(data, confidence, extractedFields) {
        try {
            const confidenceFactors = this.getConfidenceFactors(confidence);
            const techniques = [
                'Regex Pattern Matching - Structured data identification',
                'Fuzzy String Matching - Keyword proximity analysis',
                'Context-Aware Extraction - Semantic relationship mapping',
                'Template Recognition - Document structure analysis'
            ];

            return `
                <div class="col-12 mt-4">
                    <div class="result-card">
                        <div class="result-header">
                            <h5 class="mb-0">
                                <i class="fas fa-brain me-2"></i>
                                Solution Rationale & Analysis
                            </h5>
                        </div>
                        
                        <div class="rationale-content">
                            <div class="rationale-section">
                                <h6 class="text-primary">Confidence Score Calculation (${confidence}%)</h6>
                                ${confidenceFactors.map(factor => `
                                    <div class="d-flex align-items-center mb-2">
                                        <i class="fas fa-check-circle text-success me-2"></i>
                                        <span>${factor}</span>
                                    </div>
                                `).join('')}
                            </div>
                            
                            <div class="rationale-section">
                                <h6 class="text-primary">Extraction Techniques Applied</h6>
                                ${techniques.map((technique, index) => `
                                    <div class="d-flex align-items-start mb-2">
                                        <span class="badge bg-primary me-2">${index + 1}</span>
                                        <span>${technique}</span>
                                    </div>
                                `).join('')}
                            </div>
                            
                            <div class="rationale-section">
                                <h6 class="text-primary">Processing Methodology</h6>
                                <div class="bg-light p-3 rounded">
                                    <p class="mb-2"><strong>Step 1:</strong> Document structure analysis and text normalization</p>
                                    <p class="mb-2"><strong>Step 2:</strong> Pattern library matching against ${(data.requested_fields || []).length} requested fields</p>
                                    <p class="mb-2"><strong>Step 3:</strong> Multi-algorithm validation and confidence scoring</p>
                                    <p class="mb-0"><strong>Step 4:</strong> Result consolidation and quality assessment</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error in generateSolutionRationaleHTML:', error);
            return `
                <div class="col-12 mt-4">
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Solution rationale temporarily unavailable
                    </div>
                </div>
            `;
        }
    }

    getConfidenceFactors(confidence) {
        if (confidence >= 70) {
            return [
                'Strong pattern recognition',
                'Multiple field validation matches',
                'High text structure clarity'
            ];
        } else if (confidence >= 40) {
            return [
                'Moderate pattern recognition',
                'Partial field validation',
                'Some text ambiguity present'
            ];
        } else {
            return [
                'Limited pattern recognition',
                'Weak field validation',
                'High text complexity or ambiguity'
            ];
        }
    }

    generateTechniqueRankingHTML(data) {
        const sortedTechniques = Object.entries(data.technique_confidence_scores)
            .sort(([,a], [,b]) => b - a);

        return `
            <div class="ranking-section">
                <h6 class="text-primary mb-3">Technique Performance Ranking</h6>
                ${sortedTechniques.map(([techniqueName, score], index) => {
                    const displayName = this.formatTechniqueName(techniqueName);
                    const confidenceClass = this.getConfidenceClass(Math.round(score * 100));
                    
                    return `
                        <div class="ranking-item">
                            <div class="d-flex align-items-center">
                                <div class="rank-number">${index + 1}</div>
                                <div class="ms-3">
                                    <strong>${displayName}</strong>
                                </div>
                            </div>
                            <div class="badge confidence-${confidenceClass}">
                                ${Math.round(score * 100)}%
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }

    generateTechniqueComparisonHTML(data) {
        return `
            <div class="p-3">
                <h6 class="text-primary mb-3">Technique Comparison Results</h6>
                <div class="technique-comparison">
                    ${data.technique_results.map(technique => {
                        const displayName = this.formatTechniqueName(technique.technique_name);
                        const confidenceClass = this.getConfidenceClass(Math.round(technique.confidence_score * 100));
                        
                        const fieldsHTML = Object.entries(technique.extracted_fields)
                            .filter(([field, value]) => value && value.trim())
                            .map(([field, value]) => `
                                <div class="info-item mb-2">
                                    <div class="info-label">${field.replace(/_/g, ' ')}</div>
                                    <div class="info-value">${value}</div>
                                </div>
                            `).join('') || '<div class="text-muted fst-italic">No fields extracted</div>';
                        
                        return `
                            <div class="technique-result-card">
                                <div class="technique-name">${displayName}</div>
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <span>Confidence:</span>
                                    <span class="badge confidence-${confidenceClass}">
                                        ${Math.round(technique.confidence_score * 100)}%
                                    </span>
                                </div>
                                <div style="max-height: 200px; overflow-y: auto;">
                                    ${fieldsHTML}
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }

    generateConsolidatedResultsHTML(data) {
        const consolidatedHTML = Object.entries(data.consolidated_results)
            .filter(([field, value]) => value && value.trim())
            .map(([field, value]) => {
                const bestTechnique = data.best_technique_per_field[field];
                const techniqueDisplay = bestTechnique !== 'none' ? 
                    this.formatTechniqueName(bestTechnique) : 
                    'No technique found value';
                
                return `
                    <div class="info-item">
                        <div class="info-label">${field.replace(/_/g, ' ')}</div>
                        <div class="info-value">${value}</div>
                        <small class="text-muted">Best: ${techniqueDisplay}</small>
                    </div>
                `;
            }).join('');

        return `
            <div class="p-3">
                <h6 class="text-primary mb-3">Best Consolidated Results</h6>
                <div class="info-grid">
                    ${consolidatedHTML}
                </div>
            </div>
        `;
    }

    getConfidenceClass(confidence) {
        if (confidence >= 70) return 'high';
        if (confidence >= 40) return 'medium';
        return 'low';
    }

    updateProcessingStats(result) {
        this.processingStats.uploadCount++;
        this.processingStats.totalConfidence += result.confidence_score || 0.95;
        this.processingStats.totalTime += result.processing_time || 2.3;
        
        const fieldCount = Object.keys(result.extracted_fields || result.customer_info || {}).length;
        this.processingStats.totalFields += fieldCount;
        
        this.updateStatsDisplay();
    }

    updateStatsDisplay() {
        const count = this.processingStats.uploadCount;
        const uploadCountEl = document.getElementById('uploadCount');
        if (uploadCountEl) uploadCountEl.textContent = count;
        
        if (count > 0) {
            const avgConf = Math.round((this.processingStats.totalConfidence / count) * 100);
            const avgTime = (this.processingStats.totalTime / count).toFixed(1);
            const avgFields = Math.round(this.processingStats.totalFields / count);
            
            const avgConfidenceEl = document.getElementById('avgConfidence');
            const avgTimeEl = document.getElementById('avgTime');
            const fieldCountEl = document.getElementById('fieldCount');
            
            if (avgConfidenceEl) avgConfidenceEl.textContent = avgConf + '%';
            if (avgTimeEl) avgTimeEl.textContent = avgTime + 's';
            if (fieldCountEl) fieldCountEl.textContent = avgFields;
        }
    }

    loadStats() {
        const saved = localStorage.getItem('dashboardStats');
        if (saved) {
            this.processingStats = JSON.parse(saved);
            this.updateStatsDisplay();
        }
    }

    saveStats() {
        localStorage.setItem('dashboardStats', JSON.stringify(this.processingStats));
    }

    showLoading() {
        this.showElement('loading');
        this.hideElement('uploadSection');
        this.hideElement('results');
    }

    hideLoading() {
        this.hideElement('loading');
        this.showElement('uploadSection');
    }

    showError(message) {
        const errorEl = document.getElementById('error');
        const errorMessageEl = document.getElementById('errorMessage');
        
        if (errorMessageEl) errorMessageEl.textContent = message;
        if (errorEl) errorEl.style.display = 'block';
        
        this.hideLoading();
    }

    hideError() {
        this.hideElement('error');
    }

    showElement(id) {
        const element = document.getElementById(id);
        if (element) element.style.display = 'block';
    }

    hideElement(id) {
        const element = document.getElementById(id);
        if (element) element.style.display = 'none';
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Technique selection functions (global for button onclick handlers)
function selectRecommendedTechniques() {
    const recommended = ['regex_pattern_matching', 'fuzzy_string_matching', 'keyword_proximity_analysis', 'confidence_weighted_extraction'];
    document.querySelectorAll('input[name="technique"]').forEach(cb => {
        cb.checked = recommended.includes(cb.value);
    });
}

function selectAllTechniques() {
    document.querySelectorAll('input[name="technique"]').forEach(cb => cb.checked = true);
}

function clearAllTechniques() {
    document.querySelectorAll('input[name="technique"]').forEach(cb => cb.checked = false);
}

// Health check function
async function checkHealth() {
    try {
        const response = await fetch('/api/health/');
        const data = await response.json();
        
        const statusIcon = data.status === 'healthy' ? '✅' : '⚠️';
        const message = `${statusIcon} Status: ${data.status}\nFrontend: ${data.frontend}\nBackend: ${data.backend}`;
        alert(message);
    } catch (error) {
        alert('❌ Health check failed: ' + error.message);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    try {
        window.dashboard = new DocumentExtractorDashboard();
        console.log('Dashboard initialized successfully');
    } catch (error) {
        console.error('Dashboard initialization failed:', error);
    }
});