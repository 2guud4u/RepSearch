<script>
	export const product_id = 10;
    import {page} from '$app/stores';
    import "./loading.css";
    import {getItems} from "./util"
    import ItemDisplay from "$lib/components/itemDisplay/itemDisplay.svelte"
    import LoadingCard from "$lib/components/loadingCard/loadingCard.svelte"

    const searchquery = $page.params.searchTerm; 
    let promise = getItems(searchquery);
    
</script>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qc Results</title>

</head>
<body>
    
        {#await promise}
            <LoadingCard/>
        {:then data}
            <ItemDisplay items={data}/>
        {:catch error}
            <div>error{error.message}</div>
        {/await}
    
   
</body>
</html>
<style>
    
</style>


