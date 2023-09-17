<script>
	export const product_id = 10;
    import {page} from '$app/stores';
    // import {query, results} from "../../../stores";
    import { onMount } from 'svelte';
    import {goto} from "$app/navigation";
    import "./loading.css";
    import {getItems} from "./util"
    import ItemDisplay from "$lib/components/itemDisplay/itemDisplay.svelte"
    import TestComp  from '../../../lib/components/testComp/testComp.svelte';
    
    function goback(){
        controller.abort();
        goto('/')
    }
    //let searchquery = "";
    //updates searchquery
    // query.subscribe(val => {
    //     searchquery = val;
    // });
    const searchquery = $page.params.searchTerm;
    // for cancling fetch
    const controller = new AbortController();
    const signal = controller.signal;
    let promise = getItems(searchquery);
    onMount(() => {
        
        });
        let randomGifUrl = "";
        function displayRandomGif() {
            
            // Get a random index from the gifList array
            let randomIndex = Math.floor(Math.random() * 9);
            
            // Get the random GIF URL
            randomGifUrl = "./catgifs/cat" + str(randomIndex) + ".gif";
            
            // Update the src attribute of the img element with the random GIF URL
            
        }

        // Call the displayRandomGif function initially
        //displayRandomGif();
        
        // Call the displayRandomGif function every 10 seconds
        // setInterval(displayRandomGif, 5);
    
    let rand = ""
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
        <div class="gif-container center">
        <img id="random-gif" src="{randomGifUrl}" alt="Random GIF">
        <p> Here are some cats while you wait for your results!</p>
        
            <button on:click={goback} class="button">Cancel</button>
    
        </div>
        {:then data}
            <ItemDisplay items={data}/>
        {:catch error}
            <div>error{error.message}</div>
        {/await}
    
   
</body>
</html>
<style>
    
</style>


