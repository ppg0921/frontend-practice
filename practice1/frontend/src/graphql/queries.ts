import { gql } from "@apollo/client";

export type Color = {
	color: string;
	colorCode: [number, number, number];
}

export const COLOR_QUERY = gql`
  query Colors{
		colors{
			color
			colorCode
		}
	}
`;