import typescript from 'rollup-plugin-typescript';
import multiEntry from "rollup-plugin-multi-entry";


export default [{
    input: './ui/ts/index.ts',
    plugins: [
        typescript(),
        multiEntry()
    ],
    output: {
        format: 'iife',
        file: './ui/js/index.js',
        name: '' // Empty string here to create an unnamed IIFE
    },
    onwarn: function (message) {
        if (message.code === 'CIRCULAR_DEPENDENCY' || message.code === "MISSING_GLOBAL_NAME") {
            return;
        }
        console.warn(message);
    }
}];