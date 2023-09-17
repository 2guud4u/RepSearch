<script>
    import "./emptyCard.css";
    import {goto} from "$app/navigation";
    function goback(){
        goto('/')
    }
</script>
<div class="center">
    <h2> No results for ""</h2>
            <img src= "/images/EmptyCat.png">
            
            <button on:click={goback} class="empty-button" >return</button>
    
</div>