document.addEventListener('DOMContentLoaded', function() {
    var addButtons = document.getElementsByClassName('btnaddproduct');
    
    for (var i = 0; i < addButtons.length; i++) {
        addButtons[i].addEventListener('click', function() {
            var productName = this.parentNode.querySelector('p').textContent;
            document.getElementById('productname').textContent = productName;
            document.getElementById('addproductform').style.display = 'block';
            
            // Store the product name in a hidden field
            var form = document.querySelector('#addproductform form');
            var hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'product';
            hiddenInput.value = productName;
            form.appendChild(hiddenInput);
        });
    }
    
    document.querySelector('#addproductform form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        var price = document.getElementById('txtprice').value;
        var unit = document.getElementById('selunit').value;
        
        if (parseFloat(price) < 0.01) {
            alert('Price must be at least 0.01');
            return false;
        }
        
        if (unit === "") {
            alert('Please select a unit');
            return false;
        }
        
        this.submit();
    });
});
