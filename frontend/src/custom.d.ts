/*
TypeScript needs type information for imported files.
CSS files like import './App.css' are not TypeScript modules by default.
custom.d.ts tells TypeScript: “treat imports ending in .css, .scss, .sass as valid modules.”
 */

declare module '*.css';
declare module '*.scss';
declare module '*.sass';
