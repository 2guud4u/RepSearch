<script>
    import {page} from '$app/stores';
    const {product_id, review, pic} = $page.params;
</script>
<h1>{product_id} product review {review} {pic}</h1>