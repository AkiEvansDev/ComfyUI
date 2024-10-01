import { app } from "../scripts/app.js";

app.registerExtension({
    name: "default.JustBoxes",
    nodeCreated(node) {
        node.shape = 1;
    }
});