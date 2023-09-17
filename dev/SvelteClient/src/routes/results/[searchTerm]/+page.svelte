<script>
	export const product_id = 10;
    import {page} from '$app/stores';
    import "./loading.css";
    import {getItems} from "./util"
    import ItemDisplay from "$lib/components/itemDisplay/itemDisplay.svelte"
    import LoadingCard from "$lib/components/loadingCard/loadingCard.svelte"
    import EmptyCard from '../../../lib/components/emptyCard/emptyCard.svelte';
	import { onMount } from 'svelte';
    const searchquery = $page.params.searchTerm; 
    let promise;
    onMount(async()=>
    {
        promise = await getItems(searchquery);
    });
    
    
</script>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qc Results</title>

</head>
<body>
    {#if promise === undefined}
        <LoadingCard/>
    {:else}

        {#if promise.length == 0}
            <EmptyCard/>
        {:else}
            <ItemDisplay items={promise}/>
        {/if}
        
    {/if}
        
    
   
</body>
</html>
<style>
    
</style>


