import { gql } from "@apollo/client";

export interface ColorMutationSubscriptionData {
	color: string;
	colorCode: [number, number, number];
	mutation: "CREATED" | "UPDATED" | "DELETED";
}

export const COLOR_MUTATION_SUB = gql`
	subscription ColorMutationSubscription{
		colorMutated{
			color
			colorCode
			mutation
		}
	}
`;