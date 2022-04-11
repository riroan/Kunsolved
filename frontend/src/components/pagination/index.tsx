import React from 'react'
import styles from './pagination.module.scss'
import classnames from 'classnames/bind'
const cx = classnames.bind(styles)

type PaginationProps = {
    total: number
    limit: number
    page: number
    setPage: (arg0: number) => void
}

export default function Pagination({ total, limit, page, setPage }: PaginationProps) {
    const numPages = Math.ceil(total / limit)
    var left = Math.max(page - 5, 1), right
    if (numPages <= 10) {
        left = 1
        right = numPages
    } else {
        right = left === 1 ? Math.min(numPages, 10) : Math.min(page + 5, numPages)
    }

    return (
        <div className={cx('main')}>
            <button className={cx('button')} onClick={() => setPage(page - 1)} disabled={page === 1}>
                &lt;
            </button>
            {Array(right - left + 1)
                .fill(1)
                .map((_, i) => (
                    <button className={cx('button', left + i === page && 'current')} key={i + 1} onClick={() => setPage(left + i)}>
                        {left + i}
                    </button>
                ))}
            <button className={cx('button')} onClick={() => setPage(page + 1)} disabled={page === numPages}>
                &gt;
            </button>
        </div>
    )
}
