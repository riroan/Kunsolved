import React, { useState, ReactElement } from 'react'
import styles from './itemset.module.scss'
import classnames from 'classnames/bind'
import Pagination from '../pagination'
const cx = classnames.bind(styles)

type ItemSetProps = {
    data: ReactElement[]
}

export default function ItemSet({ data }: ItemSetProps) {
    const title = data[0]
    const d = data.slice(1)
    const [limit, setLimit] = useState(20)
    const [page, setPage] = useState(1)
    const offset = (page - 1) * limit
    return (
        <div className={cx('main')}>
            <div className={ cx('item')}>
                <ul className={cx('ul')}>
                    {title}
                    {d.slice(offset, offset + limit)}
                </ul>
            </div>
            <Pagination total={d.length} limit={limit} page={page} setPage={setPage} />
        </div>
    )
}
