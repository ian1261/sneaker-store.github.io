var selectedSize = "";

function openLoginForm() {
  window.open("login.html", "_blank", "width=400,height=300");
}

function selectSize(button) {
  var sizeButtons = document.querySelectorAll(".size-button");
  sizeButtons.forEach(function(sizeButton) {
    sizeButton.classList.remove("selected");
  });

  button.classList.add("selected");
  selectedSize = button.textContent;
}

function changeMainImage(imageElement) {
  var newImageSrc = imageElement.src;
  var mainImage = document.getElementById("mainProductImage");
  mainImage.src = newImageSrc;

  var smallImages = document.querySelectorAll(".extra-product-images img");
  smallImages.forEach(function(smallImage) {
    smallImage.classList.remove("selected-image");
  });

  imageElement.classList.add("selected-image");
}

function addToCart() {
if (selectedSize) {
var quantityInput = document.querySelector(".quantity-input");
var selectedQuantity = parseInt(quantityInput.value);
var price = 4380;

if (selectedQuantity >= 1 && selectedQuantity <= 5) {
  var data = {
    product_name: "Nike AIR MAX1",
    size: selectedSize, // 使用全局變量 selectedSize
    quantity: selectedQuantity,
    price: price
  };

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/add_to_cart", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        alert("已將 " + data.quantity + " 雙 " + data.size + " 尺寸的鞋子添加到購物車。");
      } else {
        alert("添加到購物車失敗。");
      }
    }
  };
  xhr.send(JSON.stringify(data));
} else {
  alert("請選擇1到5雙鞋子。");
}
} else {
alert("請選擇尺寸。");
}
}
