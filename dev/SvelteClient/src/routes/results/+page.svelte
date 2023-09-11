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
    function getRand() {
        fetch("http://127.0.0.1:5000/search")
        .then(d => d.text())
        .then(d => (rand = d));
    }
    let rand = ""
</script>
<h1>Results loading page</h1>
<h2> Search for {searchquery}</h2>
<button on:click={getRand}>Get a random number</button>
<div>hi{rand}</div>

