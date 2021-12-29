// Styles
import '../scss/main.scss'

// Libs
import $ from 'jquery'
import 'bootstrap'

// Local
import SetModalValue from './components/SetModalValue'


// Set value to modal window
$('.SetModalValue').each((_index, htmlElement) => {
    new SetModalValue($(htmlElement))
})
