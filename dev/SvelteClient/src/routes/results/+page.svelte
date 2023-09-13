<script>
	export const product_id = 10;
    import {page} from '$app/stores';
    import {query, results} from "../../stores";
    import { onMount } from 'svelte';
    import {goto} from "$app/navigation";
    
    let searchquery = "";
    query.subscribe(val => {
        searchquery = val;
    });

    onMount(() => {
        
        fetch("http://127.0.0.1:5000/search/" + searchquery)
            .then(response => {
                if (!response.ok) {
                    goto('/results/error')
                    throw new Error("HTTP error " + response.status);
                   
                }
                return response.text()
                }).then(data => {
                rand = data;
                //route to empty if empty
                console.log(rand.length)
                if(rand.length == 2){
                    goto('/results/error')
                }
                results.set(rand)
                goto('/results/'+searchquery)
            });
        
            
    
        

        
    });
    
    let rand = ""
</script>
<h1>Results loading page</h1>
<h2> Search for {searchquery}</h2>
<h1>{rand}</h1>
<h1>{$page.data}</h1>


