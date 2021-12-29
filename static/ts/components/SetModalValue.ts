import $ from 'jquery'


export default class SetModalValue {
    modal: JQuery<HTMLElement>

    constructor(modal: JQuery<HTMLElement>) {
        this.modal = modal
        let id = this.modal.attr('id')
        let triggers = $(`[href="#${id}"], [data-toggle="#${id}"]`)
        triggers.on('click', event => {
            let link = event.delegateTarget
            if (!link) {
                this.modal.hide()
                return
            }
            let value = link.getAttribute('data-whatever') || ''
            let field = this.modal.find(link.getAttribute('data-field-id') || '')
            field.val(value)
        })
    }
}
