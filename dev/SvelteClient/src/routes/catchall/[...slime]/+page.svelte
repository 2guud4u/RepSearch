<script>
    import {page} from '$app/stores';
    console.log($page.params.slime)
    const path = $page.params.slime.split('/')
</script>
dooki in catch all
{#each path as p}
    <p>{p}</p>
{/each}
