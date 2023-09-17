<script>
    import "./itemCard.css";
    export let product;
</script>

<div class="product">
    <div class="product-top">
        <h2 class="product-title">{product.title}</h2>
        <button class="toggle-button" onclick="toggleTitle(this)">...</button>
    </div>
    <p class="product-middle" id="rating">Rating:{product.rating}</p>
    <div class="product-bottom">
        <div class="button-container">
            <a  href="{product.url}" target="_blank" rel="noopener noreferrer">
                <button class="reddit">Reddit</button>
            </a>
            <a href="{product.url}" target="_blank" rel="noopener noreferrer">
                <button class="wtc">WTC</button>
            </a>
        </div>
    </div>
 </div>

<div>&nbsp;</div>