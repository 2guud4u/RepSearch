export async function getItems(query){
    const res = await fetch("http://127.0.0.1:5000/search/" + query);
    if(res.ok){
        return await res.json();
    }
    else{
        throw new Error("Error fetching items");
    }
}