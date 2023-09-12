<script>
    import {goto, beforeNavigate, afterNavigate} from "$app/navigation";
    import {query} from "../stores";
    import "./index.css"

    function handleSubmit() {
        query.set(searchVal)
        goto('/results')
    }

    $: rand = 0;
    let searchVal = "";
   


</script>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QcRepSite</title>
    
</head>
<body>
    
    <div class="searchBar">
        <div class="title">QC</div>
        <form  class="searchCont" on:submit|preventDefault={handleSubmit}>

            <input class="bar" type="text" id="searchVal" bind:value={searchVal} placeholder="Search">
            <button  class = "button bHover" on:click={handleSubmit}>Find!</button>
        </form>  
        
        <div>{searchVal}</div>
        <h1>Your number is {rand}!</h1>
    </div>
</body>

</html>