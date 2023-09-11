<script>
    import {page} from '$app/stores';
    import "./results.css";
</script>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qc Results</title>
</head>
<body>
    <div class="banner"> 
        <a  id="goBack">Go Back</a>
        <h1 id="title">Search Results</h1>
        </div>
        <div class="search-container">
        <div class="product-row">
            
         <div class="product">
            <div class="product-top">
                <h2 class="product-title"></h2>
                <button class="toggle-button" onclick="toggleTitle(this)">...</button>
            </div>
            <p class="product-middle" id="rating">Rating:</p>
            <div class="product-bottom">
                <div class="button-container">
                    <a  target="_blank" rel="noopener noreferrer">
                        <button class="reddit">Reddit</button>
                    </a>
                    <a target="_blank" rel="noopener noreferrer">
                        <button class="wtc">WTC</button>
                    </a>
                </div>
            </div>
         </div>
        
        <div>&nbsp;</div>
        
    </div>
        <form class="button-container2"  method="post">
            <button  name="fromResults" id="load-more">Load More</button>
        </form>
   </div>
   <p id="end">End of Search Results</p>

</body>
</html>
