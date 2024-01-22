import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as ec2 from 'aws-cdk-lib/aws-ec2'
import * as logs from 'aws-cdk-lib/aws-logs'
import * as iam from 'aws-cdk-lib/aws-iam'
import { DockerImageAsset } from 'aws-cdk-lib/aws-ecr-assets'

export class BedrockEcsCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create a VPC with public subnets only and 2 max azs
    const vpc = new ec2.Vpc(this, 'MyVpc', {
      maxAzs: 2,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'public-subnet',
          subnetType: ec2.SubnetType.PUBLIC
        },
      ],
    });


    // Create an ECS Cluster named "bedrock-ecs-cluster"
    const cluster = new ecs.Cluster(this, 'MyEcsCluster', {
      vpc,
      clusterName: 'bedrock-ecs-cluster',
    });

    // Build and Push Docker image to ECR
    const appImageAsset = new DockerImageAsset(this, 'MyStreamlitAppImage', {
      directory: './docker'
    });

    // Create a new Fargate service with the image from ECR and specify the service name
    const appService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'MyFargateService', {
      cluster,
      serviceName: 'ecs-bedrock-service',
      taskImageOptions: {
        image: ecs.ContainerImage.fromRegistry(appImageAsset.imageUri),
        containerPort: 8501,
      },
      publicLoadBalancer: true,
      assignPublicIp: true,
    })
  }
}
