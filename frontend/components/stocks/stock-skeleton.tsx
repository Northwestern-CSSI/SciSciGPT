export const StockSkeleton = () => {
  return (
    <div className="rounded-xl border border-gray-300 bg-gray-100 p-4 text-gray-400">
      <div className="float-right inline-block w-fit rounded-full bg-gray-300 px-2 py-1 text-xs text-transparent">
        xxxxxxx
      </div>
      <div className="mb-1 w-fit rounded-md bg-gray-300 text-lg text-transparent">
        xxxx
      </div>
      <div className="w-fit rounded-md bg-gray-300 text-3xl font-bold text-transparent">
        xxxx
      </div>
      <div className="text mt-1 w-fit rounded-md bg-gray-300 text-xs text-transparent">
        xxxxxx xxx xx xxxx xx xxx
      </div>

      <div className="relative -mx-4 cursor-col-resize">
        <div style={{ height: 100 }}></div>
      </div>
    </div>
  )
}
