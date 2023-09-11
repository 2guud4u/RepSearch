import {comments} from "$lib/comments.js";
import {json} from "@sveltejs/kit";

export function GET() {
    return json(comments);
}