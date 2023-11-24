import { gql } from "@apollo/client";

export interface CreateColorVariables{
	input:{
		color:string,
		colorCode: [number, number, number],
	},
}

export interface DeleteColorVariables{
	input:{
		color:string,
	},
}

export interface ChangeColorCodeMutationResponseDataType {
	ok:boolean;
}

export interface ChangeColorCodeMutationVariables{
	color: string;
	colorCode: [number, number, number];
}

export const CREATE_COLOR_MUTATION = gql`
	mutation CreateColor($input: CreateColorInput!){
		createColor(input: $input)
	}
`;

export const CHANGE_COLOR_CODE = gql`
	mutation UpdateColor($input: UpdateColorInput!){
		updateColor(input: $input)
	}
`;

export const DELETE_COLOR_MUTATION = gql`
	mutation DeleteColor($input: DeleteColorInput!){
		deleteColor(input: $input)
	}
`;