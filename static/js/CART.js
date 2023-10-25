let purchases = [{% for purchase in purchases %}{ "quantity": {{ purchase.quantity }}, "price": {{ purchase.price }} }{% if not loop.last %}, {% endif %}{% endfor %}];

function updateTotal() {
    const total = purchases.reduce((acc, item) => {
        return acc + (item.quantity * item.price);
    }, 0);
    
    const totalElement = document.getElementById('total');
    totalElement.textContent = `總計金額：${total} 元`;
}

function removeItem(element, productName, size) {
    // ...

    fetch('/remove_from_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nickname: '{{ session["nickname"] }}',
            product_name: productName,
            size: size
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        location.reload(); // 在成功刪除後重新加載頁面
    })
    .catch(error => console.error('Error:', error));
}
// 初始計算總金額
updateTotal();        
