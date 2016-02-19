
function KeyLogger( target ) {
  this.target = target;
  this.log = [];
console.log('this=', this);

  var that = this;
console.log('that=', that);
  this.target.off( "keydown" ).on( "keydown", function( event ) {
    that.log.push( event.keyCode );
console.log('ev this=', this);
console.log('ev that=', that);
  });
console.log('last this=', this);
}


