import React, { useState, ReactElement } from 'react'
import styles from './itemset.module.scss'
import classnames from 'classnames/bind'
import Pagination from '../pagination'
const cx = classnames.bind(styles)

type ItemSetProps = {
    data: ReactElement[]
    usePagination: boolean
}

export default function ItemSet({ data, usePagination }: ItemSetProps) {
    const title = data[0]
    const d = data.slice(1)
    const limit = 20
    const [page, setPage] = useState(1)
    const offset = (page - 1) * limit
    return (
        <div className={cx('main')}>
            <div className={cx('item')}>
                <ul className={cx('ul')}>
                    {title}
                    {usePagination ? d.slice(offset, offset + limit) : d}
                </ul>
            </div>
            {usePagination && <Pagination total={d.length} limit={limit} page={page} setPage={setPage} />}
        </div>
    )
}

ItemSet.defaultProps = {
    usePagination: true,
}
