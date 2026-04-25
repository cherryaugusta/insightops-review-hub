import type { ReactNode } from "react";

type Column<T> = {
  header: string;
  cell: (item: T) => ReactNode;
};

type DataTableProps<T> = {
  data: T[];
  columns: Column<T>[];
};

export function DataTable<T>({ data, columns }: DataTableProps<T>) {
  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.header}>{column.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column.header}>{column.cell(item)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
