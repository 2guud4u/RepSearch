<script>
    import {goto} from "$app/navigation";
	import { get } from "svelte/store";
    function goback(){
        goto('/')
    }
    function getRandomGif(max) {
        return  "/images/catgifs/cat"+ Math.floor(Math.random() * max).toString() +".gif";
    }
    $: randomGifUrl = getRandomGif(9)
    
    setInterval(function(){
        randomGifUrl = getRandomGif(9)
    }, 3000);
</script>
<div class="gif-container center">
    <img id="random-gif" src="{randomGifUrl}" alt="Random GIF">
    <p style="color:white;"> Here are some cats while you wait for your results!</p>
    
        <button on:click={goback} class="button">Cancel</button>

</div>