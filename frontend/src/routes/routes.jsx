import { Route } from 'react-router-dom'

import { Home } from '../pages/Home'
import { Register } from '../pages/Register'
import { SensorList } from '../pages/SensorList'
import { SensorDetail } from '../pages/SensorDetails'

export const routes = () => {
  return (
    <>
        <Route path='/' element={<Home />} />
       <Route path='/register' element={<Register />} />
       <Route path="/sensors" element={<SensorList />} />
       <Route path="/sensors/:id" element={<SensorDetail />} />
    </>
   
    
  )
}
