function updateSidebar(data) {
    const contentArea = document.getElementById('content-area');
    
    if (!data) {
        contentArea.innerHTML = '<div class="status-message">No data available</div>';
        return;
    }
    
    let html = `
        <div class="company-section">
            <div class="company-id">ID: ${data.id}</div>
            <div class="company-name">${data.company_name}</div>
            
            <div class="info-field" onclick="toggleField(this, 'website')">
                <div class="field-label">🔗 Website</div>
                <div class="field-value">${data.website || 'Not found'}</div>
            </div>
            
            <div class="info-field" onclick="toggleField(this, 'phone')">
                <div class="field-label">📞 Phone</div>
                <div class="field-value">${data.phone || 'Not found'}</div>
            </div>
            
            <div class="info-field" onclick="toggleField(this, 'email')">
                <div class="field-label">📧 Email</div>
                <div class="field-value">${data.email || 'Not found'}</div>
            </div>
            
            <div class="info-field" onclick="toggleField(this, 'about')">
                <div class="field-label">ℹ️ About</div>
                <div class="field-value">${data.about || 'Not found'}</div>
            </div>
        </div>
        
        <div class="status-message">
            Click on any field to verify or highlight it
        </div>
    `;
    
    contentArea.innerHTML = html;
}

function toggleField(element, fieldType) {
    // Toggle selected class
    element.classList.toggle('selected');
    
    // Send message to parent window (for Python to capture)
    window.parent.postMessage({
        type: 'field_clicked',
        field: fieldType,
        selected: element.classList.contains('selected')
    }, '*');
    
    console.log(`Field ${fieldType} ${element.classList.contains('selected') ? 'selected' : 'deselected'}`);
}

// Listen for messages from Python
window.addEventListener('message', function(event) {
    if (event.data.type === 'update_data') {
        updateSidebar(event.data.data);
    }
});
