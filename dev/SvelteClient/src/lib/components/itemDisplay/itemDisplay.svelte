<script>
    import ItemCard from '$lib/components/itemCard/itemCard.svelte';
    import "./itemDisplay.css";
    import {goto} from "$app/navigation";
    function goback(){
        goto('/')
    }
    export let items;
    

    
</script>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qc Results</title>
</head>
<body>
    <div class="banner"> 
        
        <button on:click={goback} id="goback">Go Back</button>
        <h1 id="title">Search Results</h1>
        </div>
        <div class="search-container">
        <div class="product-row">
        {#each items as product}
            <ItemCard product={product} />
        {/each}
    </div>
        <form class="button-container2"  method="post">
            <button  name="fromResults" id="load-more">Load More</button>
        </form>
   </div>
   <p id="end">End of Search Results</p>
   
</body>
</html>
