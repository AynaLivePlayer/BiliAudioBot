import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  {path: '/', component: 'Home'},
  {path: '/textinfo', component: 'TextInfo'},
  {path: '/currentplaying', component: 'CurrentPlaying'},
  {path: '/currentcover', component: 'CurrentCover'},
  {path: '/currentlyric', component: 'CurrentLyric'},
  {path: '*', component: 'NotFound'}
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/views/${route.component}.vue`)
  }
})
Vue.use(Router)
export default new Router({
  routes,
  mode: 'history'
})
