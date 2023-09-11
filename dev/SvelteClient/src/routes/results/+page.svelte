<script>
	export const product_id = 10;
    import {page} from '$app/stores';
    import {query} from "../../stores";
    import { onMount } from 'svelte';
    
    let searchquery = "";
    query.subscribe(val => {
        searchquery = val;
    });

    onMount(() => {
        console.log("searchquery: " + searchquery);
    });
</script>
<h1>Results loading page</h1>
<h2> Search for {searchquery}</h2>

