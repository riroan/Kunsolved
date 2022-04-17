import { configureStore, getDefaultMiddleware } from '@reduxjs/toolkit'
import { schooljoonApi } from '../services/schooljoon'
import { setupListeners } from '@reduxjs/toolkit/dist/query'

export const store = configureStore({
    reducer: {
        [schooljoonApi.reducerPath]: schooljoonApi.reducer,
    },
    middleware: getDefaultMiddleware => getDefaultMiddleware().concat(schooljoonApi.middleware),
})


setupListeners(store.dispatch)