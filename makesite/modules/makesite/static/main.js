require("zeta://zeta.js");

zeta.blocks['toggle'] = function(params){
    var self = this, target = $(params.rel);
    self.click(function(e){
        self.toggleClass('toggle_active');
        target.toggle('slow');
        return false;
    });
}
