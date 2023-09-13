<script>
    import {page} from '$app/stores';
    import "./results.css";
    import {results} from "../../../stores";
    // let result = []
    // results.subscribe(val => {
    //     result = val;
    //     console.log(result);
    // });
    export let data;
    console.log(data);
    let jsondata = JSON.parse(data.result);
    
</script>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qc Results</title>
</head>
{#if data.result}
<body>
    <div class="banner"> 
        
        <div  id="goBack">Go Back</div>
        <h1 id="title">Search Results</h1>
        </div>
        <div class="search-container">
        <div class="product-row">
        {#each jsondata as product}
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
        {/each}
    </div>
        <form class="button-container2"  method="post">
            <button  name="fromResults" id="load-more">Load More</button>
        </form>
   </div>
   <p id="end">End of Search Results</p>
   
</body>
{/if}
</html>
