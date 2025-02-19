import { app } from "../scripts/app.js";

app.registerExtension({
    name: "default.JustBoxes",
    nodeCreated(node) {
        node.shape = 1;
        if (node.comfyClass == "Reroute") {
            console.log(node);
        } else if (node.comfyClass == "Reroute (rgthree)") {
            node.color = "#353535";
            node.bgcolor = "#353535";
        } else {
            node.color = "#353535";
            node.bgcolor = "#212121";
        }
    }
});