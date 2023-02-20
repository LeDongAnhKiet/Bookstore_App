function isEmpty(value){
    return value === null || typeof(value) === 'undefined' || value === ''
}

function addToCart(id, name, price) {
    let a = document?.querySelector('#numberToCart')?.value
    if (a === undefined || a < 1)
        a = 1
    if (a > 10)
        a = 10
    console.log(a)
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price,
            "quantity": parseInt(a)
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then((data) => {
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    })
}

function updateCart(bookId, obj) {
    fetch(`/api/cart/${bookId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then((data) => {
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let a = document.getElementsByClassName("cart-amount")
        for (let i = 0; i < a.length; i++)
            a[i].innerText = data.total_amount.toLocaleString("en-US")
    }).catch(err => console.error(err)) // promise
}

function deleteCart(bookId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/api/cart/${bookId}`, {
            method: "delete"
        }).then(res => res.json()).then((data) => {
            let d = document.getElementsByClassName("cart-counter")
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let a = document.getElementsByClassName("cart-amount")
            for (let i = 0; i < a.length; i++)
                a[i].innerText = data.total_amount.toLocaleString("en-US")

            let e = document.getElementById(`cart${bookId}`)
            e.style.display = "none"
        }).catch(err => console.error(err)) // promise
    }

}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán không?")) {
        fetch("/pay").then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload()
        })
    }

}

function preorder() {
    if (confirm("Bạn chắc chắn đặt hàng không?")) {
        fetch("/preorder").then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload()
        })
    }

}
// Lấy radio button đê chọn cách thanh toán
function MakePayment() {
            var ele = document.getElementsByName('ordertype');

            for(i = 0; i < ele.length; i++) {
                if(ele[i].checked)
                    a = +ele[i].value;
            }
            if (a == "1")
                pay()
            else
                preorder()
        }

