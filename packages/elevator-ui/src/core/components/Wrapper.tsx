import { useMemo, type ReactNode } from "react";

import { cleanObject } from "../utils/cleanObject";

const SPACING = 7;

export const Wrapper = ({
  backgroundColor,
  border,
  children,
  flex,
  height,
  isRow,
  m,
  mBottom,
  mLeft,
  mRight,
  mTop,
  p,
  pBottom,
  pLeft,
  pRight,
  pTop,
  width,
}: WrapperPropsModel) => {
  const style: React.CSSProperties = useMemo(
    () =>
      cleanObject({
        backgroundColor,
        border: border ? "1px solid black" : undefined,
        display: "flex",
        flex,
        flexDirection: isRow ? "row" : "column",
        height,
        marginBottom:
          m === true ? SPACING : mBottom === true ? SPACING : (m ?? mBottom),
        marginLeft:
          m === true ? SPACING : mLeft === true ? SPACING : (m ?? mLeft),
        marginRight:
          m === true ? SPACING : mRight === true ? SPACING : (m ?? mRight),
        marginTop: m === true ? SPACING : mTop === true ? SPACING : (m ?? mTop),
        paddingBottom:
          p === true ? SPACING : pBottom === true ? SPACING : (p ?? pBottom),
        paddingLeft:
          p === true ? SPACING : pLeft === true ? SPACING : (p ?? pLeft),
        paddingRight:
          p === true ? SPACING : pRight === true ? SPACING : (p ?? pRight),
        paddingTop:
          p === true ? SPACING : pTop === true ? SPACING : (p ?? pTop),
        width,
      }),
    [
      backgroundColor,
      border,
      flex,
      height,
      m,
      mBottom,
      mLeft,
      mRight,
      mTop,
      p,
      pBottom,
      pLeft,
      pRight,
      pTop,
      width,
    ],
  );
  return <div style={style}>{children}</div>;
};

export type WrapperPropsModel = {
  backgroundColor?: string;
  border?: true;
  children?: ReactNode;
  flex?: number;
  height?: number;
  isRow?: boolean;
  m?: number | true;
  mBottom?: number | true;
  mLeft?: number | true;
  mRight?: number | true;
  mTop?: number | true;
  p?: number | true;
  pBottom?: number | true;
  pLeft?: number | true;
  pRight?: number | true;
  pTop?: number | true;
  width?: number;
};
