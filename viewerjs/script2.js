var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(60, 1, 1, 1000);
camera.position.set(2, 2, 2);
var renderer = new THREE.WebGLRenderer({
  antialias: true
});
renderer.setClearColor(0x808080);
var canvas = renderer.domElement
document.body.appendChild(canvas);

var controls = new THREE.OrbitControls(camera, renderer.domElement);

var light = new THREE.HemisphereLight( 0xffffbb, 0x080820, 1 );
scene.add( light );

// var loader = new THREE.GLTFLoader();
// loader.load( 'https://threejs.org/examples/models/gltf/Horse.glb', function ( gltf ) {
// loader.load( './freecad.glb', function ( gltf ) {

var loader = new THREE.JSONLoader();
// var loader = new THREE.LegacyJSONLoader();
loader.load( './collar.tjs', function ( gltf ) {
// loader.load( './collar.json', function ( gltf ) {
// var loader = new THREE.VRMLLoader();
// loader.load( './collar.vrml', function ( gltf ) {
// var loader = new THREE.STLLoader();
// loader.load( './collar.stl', function ( gltf ) {
  console.log(gltf);
  //gltf.scene.position.z = -10;
  scene.add( gltf.scene );

}, undefined, function ( error ) {

  console.error( error );

} );




render();

function render() {
  if (resize(renderer)) {
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
  }
  renderer.render(scene, camera);
  requestAnimationFrame(render);
}

function resize(renderer) {
  const canvas = renderer.domElement;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  const needResize = canvas.width !== width || canvas.height !== height;
  if (needResize) {
    renderer.setSize(width, height, false);
  }
  return needResize;
}
