import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const schooljoonApi = createApi({
    reducerPath: 'schooljoonApi',
    baseQuery: fetchBaseQuery({ baseUrl: 'https://api.riroan.com' }),
    endpoints: builder => ({
        getData: builder.query({
            query: name => name,
        }),
    }),
})

export const { useGetDataQuery } = schooljoonApi
