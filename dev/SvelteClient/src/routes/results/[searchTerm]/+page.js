import {results} from "../../../stores";

export function load(){
    let result = []
    results.subscribe(val => {
        result = val;
    });
    return {
        result
    }
}