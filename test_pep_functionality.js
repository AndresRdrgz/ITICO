// Test script to verify PEP checkbox functionality
console.log('Testing PEP checkbox functionality...');

// Wait for page to load
setTimeout(() => {
    // Simulate clicking the Add Member button
    const addMemberBtn = document.getElementById('add-member-btn');
    if (addMemberBtn) {
        addMemberBtn.click();
        console.log('Add member button clicked');
        
        // Wait for modal to load
        setTimeout(() => {
            const pepCheckbox = document.querySelector('#miembro-modal input[name="es_pep"]');
            const pepPositionContainer = document.getElementById('pep-position-container');
            
            if (pepCheckbox && pepPositionContainer) {
                console.log('PEP elements found');
                console.log('PEP checkbox checked:', pepCheckbox.checked);
                console.log('Position container hidden:', pepPositionContainer.classList.contains('hidden'));
                
                // Test checking the PEP checkbox
                pepCheckbox.checked = true;
                pepCheckbox.dispatchEvent(new Event('change'));
                
                console.log('After checking PEP:');
                console.log('Position container hidden:', pepPositionContainer.classList.contains('hidden'));
                
                // Test unchecking the PEP checkbox
                pepCheckbox.checked = false;
                pepCheckbox.dispatchEvent(new Event('change'));
                
                console.log('After unchecking PEP:');
                console.log('Position container hidden:', pepPositionContainer.classList.contains('hidden'));
            } else {
                console.log('PEP elements not found');
                console.log('pepCheckbox:', pepCheckbox);
                console.log('pepPositionContainer:', pepPositionContainer);
            }
        }, 2000);
    } else {
        console.log('Add member button not found');
    }
}, 1000);
