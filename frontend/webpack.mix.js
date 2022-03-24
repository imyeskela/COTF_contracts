let mix = require('laravel-mix');

mix.options({
    fileLoaderDirs:  {
        fonts: '../static/fonts'
    }
});

mix.setPublicPath("../static").sass('sass/app.scss','css');
mix.setPublicPath("../static").sass('sass/lib.scss', 'css');
mix.setPublicPath("../static").js('js/app.js', 'js');