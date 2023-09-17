<script>
    import ItemCard from '$lib/components/itemCard/itemCard.svelte';
    export let items;
</script>

<h1>I AM A TEST COMPONENT{items}</h1>
{#each items as product}
            <ItemCard product={product} />
{/each}