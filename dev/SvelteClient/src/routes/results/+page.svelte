<script>
	export const product_id = 10;
    import {page} from '$app/stores';
    import {query, results} from "../../stores";
    import { onMount } from 'svelte';
    import {goto} from "$app/navigation";
    import "./loading.css";

 
    function goback(){
        controller.abort();
        goto('/')
    }

    let searchquery = "";
    //updates searchquery
    query.subscribe(val => {
        searchquery = val;
    });
    // for cancling fetch
    const controller = new AbortController();
    const signal = controller.signal;
    onMount(() => {
        
        fetch("http://127.0.0.1:5000/search/" + searchquery, {signal})
            .then(response => {
                if (!response.ok) {
                    goto('/results/error')
                    throw new Error("HTTP error " + response.status);
                   
                }
                return response.text()
                }).then(data => {
                rand = data;
                //route to empty if empty
                
                if(rand.length == 2){
                    goto('/results/error')
                }
                results.set(rand)
                goto('/results/'+searchquery)
            });
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
        setInterval(displayRandomGif, 5);
    
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
    <div class="gif-container center">
      <img id="random-gif" src="{randomGifUrl}" alt="Random GIF">
      <p> Here are some cats while you wait for your results!</p>
     
        <button on:click={goback} class="button">Cancel</button>
  
    </div>
</body>
</html>
<style>
    
</style>


