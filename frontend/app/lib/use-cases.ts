
export interface UseCase {
  id: string;
  name: string;
  icon: string;
  tagline: string;
  description: string;
  heroTitle: string;
  heroSubtitle: string;
  primaryColor: string;
  secondaryColor: string;
  features: Array<{
    title: string;
    description: string;
    icon: string;
  }>;
  agentGroups: Array<{
    title: string;
    icon: string;
    color: string;
    agents: Array<{
      name: string;
      type?: string;
      description: string;
    }>;
  }>;
  ctaText: string;
}

export const USE_CASES: UseCase[] = [
  {
    id: 'compliance',
    name: 'Compliance & Regulatory',
    icon: 'Shield',
    tagline: 'Enterprise Multi-Agent Platform',
    description: 'Automate compliance workflows, reduce risk, and make intelligent business decisions',
    heroTitle: 'Intelligent Compliance',
    heroSubtitle: 'Automation',
    primaryColor: 'blue',
    secondaryColor: 'purple',
    features: [
      {
        title: 'Compliance Intelligence',
        description: 'Multi-agent analysis of regulations, policies, and documents with comprehensive risk assessment.',
        icon: 'Shield'
      },
      {
        title: 'Real-Time Processing',
        description: 'Monitor workflow execution in real-time with live agent status updates and progress tracking.',
        icon: 'Zap'
      },
      {
        title: 'Multi-Agent Collaboration',
        description: '19 specialized AI agents working in harmony across reasoning, memory, learning, and coordination domains.',
        icon: 'Users'
      }
    ],
    agentGroups: [
      {
        title: 'Core Compliance Agents',
        icon: 'Shield',
        color: 'blue',
        agents: [
          { name: 'ReAct', type: 'Reasoning & Acting', description: 'Structured reasoning and compliance analysis with action planning' },
          { name: 'Evaluator', type: 'Quality Assessment', description: 'Risk scoring and compliance evaluation with confidence metrics' },
          { name: 'Debate', type: 'Multi-Perspective', description: 'Diverse viewpoint generation and stakeholder modeling' },
          { name: 'Governor', type: 'Governance', description: 'Policy enforcement and preflight validation checks' },
        ]
      },
      {
        title: 'Advanced Reasoning Agents',
        icon: 'Network',
        color: 'purple',
        agents: [
          { name: 'Chain of Thought', description: 'Step-by-step logical analysis with transparent reasoning' },
          { name: 'Tree of Thought', description: 'Branching reasoning for exploring multiple solution paths' },
          { name: 'Planning', description: 'Strategic planning and workflow optimization' },
          { name: 'Reflection', description: 'Self-assessment and iterative quality improvement' },
        ]
      },
      {
        title: 'Memory & Learning Agents',
        icon: 'Network',
        color: 'green',
        agents: [
          { name: 'Memory', description: 'Context storage and historical knowledge management' },
          { name: 'Adaptive Memory', description: 'Dynamic memory with intelligent priority management' },
          { name: 'Curriculum', description: 'Progressive learning with difficulty adaptation' },
          { name: 'Meta Evolver', description: 'Strategy evolution and adaptive optimization' },
        ]
      },
      {
        title: 'Coordination & Execution Agents',
        icon: 'Users',
        color: 'orange',
        agents: [
          { name: 'Multi-Agent', description: 'Parallel execution and result aggregation' },
          { name: 'Swarm', description: 'Collective intelligence and consensus building' },
          { name: 'Hierarchical', description: 'Structured task delegation and supervision' },
          { name: 'Toolformer', description: 'Tool selection and external API integration' },
        ]
      },
      {
        title: 'Specialized & Autonomous Agents',
        icon: 'Zap',
        color: 'yellow',
        agents: [
          { name: 'Generative', description: 'Content generation and synthetic scenario creation' },
          { name: 'Voyager', description: 'Exploration and novel solution discovery' },
          { name: 'Auto Loop', description: 'Autonomous operation and self-directed execution' },
        ]
      }
    ],
    ctaText: 'Transform Your Compliance Process'
  },
  {
    id: 'customer-support',
    name: 'Customer Support & Service',
    icon: 'Headphones',
    tagline: 'AI-Powered Support Platform',
    description: 'Deliver exceptional customer experiences with intelligent automation and multi-agent support',
    heroTitle: 'Intelligent Customer',
    heroSubtitle: 'Support',
    primaryColor: 'green',
    secondaryColor: 'teal',
    features: [
      {
        title: 'Intelligent Ticket Routing',
        description: 'AI agents automatically categorize, prioritize, and route support tickets to the right team or agent.',
        icon: 'MessageSquare'
      },
      {
        title: 'Real-Time Response',
        description: 'Multi-agent collaboration provides instant, accurate responses with consistent quality across all channels.',
        icon: 'Zap'
      },
      {
        title: 'Continuous Learning',
        description: 'Agents learn from every interaction to improve response quality and reduce resolution time.',
        icon: 'Brain'
      }
    ],
    agentGroups: [
      {
        title: 'Customer Interaction Agents',
        icon: 'MessageSquare',
        color: 'green',
        agents: [
          { name: 'ReAct', type: 'Support Reasoning', description: 'Analyze customer issues and determine optimal response strategies' },
          { name: 'Chain of Thought', description: 'Step-by-step troubleshooting with clear explanations' },
          { name: 'Debate', type: 'Solution Exploration', description: 'Generate multiple solution approaches for complex issues' },
          { name: 'Evaluator', type: 'Quality Control', description: 'Assess response quality and customer satisfaction metrics' },
        ]
      },
      {
        title: 'Knowledge & Learning Agents',
        icon: 'Brain',
        color: 'blue',
        agents: [
          { name: 'Memory', description: 'Store customer history and preferences for personalized service' },
          { name: 'Adaptive Memory', description: 'Learn from patterns to anticipate customer needs' },
          { name: 'Curriculum', description: 'Progressive learning from simple to complex support scenarios' },
          { name: 'Meta Evolver', description: 'Optimize support strategies based on performance data' },
        ]
      },
      {
        title: 'Coordination Agents',
        icon: 'Users',
        color: 'purple',
        agents: [
          { name: 'Multi-Agent', description: 'Coordinate multiple specialists for complex support cases' },
          { name: 'Hierarchical', description: 'Escalate issues through appropriate support tiers' },
          { name: 'Swarm', description: 'Collective problem-solving for challenging customer issues' },
          { name: 'Planning', description: 'Strategic resolution planning for multi-step issues' },
        ]
      },
      {
        title: 'Automation & Integration Agents',
        icon: 'Zap',
        color: 'orange',
        agents: [
          { name: 'Toolformer', description: 'Integrate with CRM, ticketing, and communication platforms' },
          { name: 'Auto Loop', description: 'Autonomous ticket monitoring and proactive issue resolution' },
          { name: 'Generative', description: 'Generate knowledge base articles from support interactions' },
        ]
      },
      {
        title: 'Quality & Improvement Agents',
        icon: 'TrendingUp',
        color: 'red',
        agents: [
          { name: 'Reflection', description: 'Analyze support quality and identify improvement areas' },
          { name: 'Governor', type: 'Quality Standards', description: 'Ensure responses meet quality and brand guidelines' },
          { name: 'Tree of Thought', description: 'Explore alternative solutions for better customer outcomes' },
          { name: 'Voyager', description: 'Discover innovative support approaches from edge cases' },
        ]
      }
    ],
    ctaText: 'Elevate Your Customer Support'
  },
  {
    id: 'sales-automation',
    name: 'Sales & Revenue Automation',
    icon: 'TrendingUp',
    tagline: 'AI-Powered Sales Platform',
    description: 'Accelerate sales cycles, optimize pipelines, and close more deals with intelligent automation',
    heroTitle: 'Intelligent Sales',
    heroSubtitle: 'Acceleration',
    primaryColor: 'purple',
    secondaryColor: 'pink',
    features: [
      {
        title: 'Lead Intelligence',
        description: 'Multi-agent analysis of leads with scoring, qualification, and personalized outreach strategies.',
        icon: 'Target'
      },
      {
        title: 'Pipeline Optimization',
        description: 'Real-time monitoring and optimization of sales pipelines with predictive analytics and bottleneck detection.',
        icon: 'BarChart'
      },
      {
        title: 'Smart Automation',
        description: 'Automated follow-ups, meeting scheduling, and proposal generation that learns from your best performers.',
        icon: 'Sparkles'
      }
    ],
    agentGroups: [
      {
        title: 'Lead Generation & Qualification',
        icon: 'Target',
        color: 'purple',
        agents: [
          { name: 'ReAct', type: 'Lead Analysis', description: 'Analyze prospect behavior and determine engagement strategies' },
          { name: 'Evaluator', type: 'Lead Scoring', description: 'Score and prioritize leads based on conversion probability' },
          { name: 'Tree of Thought', description: 'Explore multiple outreach strategies for different prospect segments' },
          { name: 'Planning', description: 'Develop strategic account penetration plans' },
        ]
      },
      {
        title: 'Sales Intelligence',
        icon: 'Brain',
        color: 'blue',
        agents: [
          { name: 'Memory', description: 'Maintain comprehensive prospect and customer interaction history' },
          { name: 'Adaptive Memory', description: 'Learn buying patterns and preferences over time' },
          { name: 'Debate', type: 'Strategy Development', description: 'Generate diverse sales approaches for complex deals' },
          { name: 'Reflection', description: 'Analyze win/loss patterns to improve sales tactics' },
        ]
      },
      {
        title: 'Deal Orchestration',
        icon: 'Users',
        color: 'green',
        agents: [
          { name: 'Multi-Agent', description: 'Coordinate across sales, marketing, and support teams' },
          { name: 'Hierarchical', description: 'Manage complex enterprise sales with multiple stakeholders' },
          { name: 'Swarm', description: 'Collaborative problem-solving for deal obstacles' },
          { name: 'Governor', type: 'Deal Validation', description: 'Ensure deals meet qualification and pricing standards' },
        ]
      },
      {
        title: 'Sales Automation',
        icon: 'Zap',
        color: 'orange',
        agents: [
          { name: 'Toolformer', description: 'Integrate with CRM, email, calendar, and proposal tools' },
          { name: 'Auto Loop', description: 'Autonomous follow-up and pipeline management' },
          { name: 'Generative', description: 'Generate personalized emails, proposals, and presentations' },
        ]
      },
      {
        title: 'Performance Optimization',
        icon: 'TrendingUp',
        color: 'red',
        agents: [
          { name: 'Curriculum', description: 'Progressive training from simple to complex sales scenarios' },
          { name: 'Meta Evolver', description: 'Optimize sales processes based on performance data' },
          { name: 'Voyager', description: 'Discover innovative sales tactics from successful outliers' },
          { name: 'Chain of Thought', description: 'Detailed deal analysis with clear next-step recommendations' },
        ]
      }
    ],
    ctaText: 'Accelerate Your Sales Pipeline'
  },
  {
    id: 'research-analysis',
    name: 'Research & Data Analysis',
    icon: 'Search',
    tagline: 'AI Research Assistant Platform',
    description: 'Transform complex data into actionable insights with multi-agent research and analysis',
    heroTitle: 'Intelligent Research',
    heroSubtitle: 'Analysis',
    primaryColor: 'indigo',
    secondaryColor: 'cyan',
    features: [
      {
        title: 'Deep Research',
        description: 'Multi-agent exploration of topics with comprehensive literature review and synthesis.',
        icon: 'Search'
      },
      {
        title: 'Data Analysis',
        description: 'Advanced statistical analysis and pattern recognition across structured and unstructured data.',
        icon: 'BarChart3'
      },
      {
        title: 'Insight Generation',
        description: 'Automated report generation with visualizations, findings, and actionable recommendations.',
        icon: 'Lightbulb'
      }
    ],
    agentGroups: [
      {
        title: 'Research Agents',
        icon: 'Search',
        color: 'indigo',
        agents: [
          { name: 'ReAct', type: 'Research Planning', description: 'Structured research methodology with systematic data gathering' },
          { name: 'Tree of Thought', description: 'Explore multiple research hypotheses and methodologies' },
          { name: 'Voyager', description: 'Discover novel connections and unexplored research angles' },
          { name: 'Planning', description: 'Design comprehensive research strategies and timelines' },
        ]
      },
      {
        title: 'Analysis Agents',
        icon: 'BarChart3',
        color: 'blue',
        agents: [
          { name: 'Chain of Thought', description: 'Step-by-step logical analysis of complex datasets' },
          { name: 'Evaluator', type: 'Data Quality', description: 'Assess data quality, reliability, and statistical significance' },
          { name: 'Debate', type: 'Interpretation', description: 'Consider multiple interpretations of research findings' },
          { name: 'Reflection', description: 'Critical review of methodology and conclusions' },
        ]
      },
      {
        title: 'Knowledge Management',
        icon: 'Brain',
        color: 'purple',
        agents: [
          { name: 'Memory', description: 'Maintain comprehensive research databases and citations' },
          { name: 'Adaptive Memory', description: 'Learn domain-specific patterns and relationships' },
          { name: 'Curriculum', description: 'Progressive learning from basic to advanced research topics' },
          { name: 'Meta Evolver', description: 'Optimize research methodologies based on outcomes' },
        ]
      },
      {
        title: 'Collaboration Agents',
        icon: 'Users',
        color: 'green',
        agents: [
          { name: 'Multi-Agent', description: 'Coordinate multiple research streams in parallel' },
          { name: 'Swarm', description: 'Collective intelligence for complex problem-solving' },
          { name: 'Hierarchical', description: 'Manage large-scale research projects with sub-teams' },
        ]
      },
      {
        title: 'Synthesis & Reporting',
        icon: 'FileText',
        color: 'orange',
        agents: [
          { name: 'Generative', description: 'Generate comprehensive research reports and summaries' },
          { name: 'Toolformer', description: 'Integrate with data sources, APIs, and visualization tools' },
          { name: 'Governor', type: 'Quality Control', description: 'Ensure research meets academic and quality standards' },
          { name: 'Auto Loop', description: 'Autonomous monitoring of research domains for updates' },
        ]
      }
    ],
    ctaText: 'Accelerate Your Research'
  },
  {
    id: 'generic',
    name: 'Multi-Purpose AI Platform',
    icon: 'Sparkles',
    tagline: 'Versatile Multi-Agent Platform',
    description: 'Adapt to any business challenge with flexible AI agent orchestration',
    heroTitle: 'Intelligent Enterprise',
    heroSubtitle: 'Automation',
    primaryColor: 'slate',
    secondaryColor: 'zinc',
    features: [
      {
        title: 'Flexible Architecture',
        description: 'Adapt to any business process with configurable agent workflows and custom task orchestration.',
        icon: 'Settings'
      },
      {
        title: 'Scalable Intelligence',
        description: 'Deploy agents across any domain with automatic scaling and resource optimization.',
        icon: 'TrendingUp'
      },
      {
        title: 'Universal Integration',
        description: 'Connect with any tool, API, or data source through flexible integration framework.',
        icon: 'Plug'
      }
    ],
    agentGroups: [
      {
        title: 'Core Intelligence Agents',
        icon: 'Brain',
        color: 'slate',
        agents: [
          { name: 'ReAct', type: 'Reasoning & Acting', description: 'General-purpose reasoning with action planning' },
          { name: 'Chain of Thought', description: 'Step-by-step logical analysis for any domain' },
          { name: 'Tree of Thought', description: 'Explore multiple solution paths for complex problems' },
          { name: 'Planning', description: 'Strategic planning and workflow optimization' },
        ]
      },
      {
        title: 'Evaluation & Quality',
        icon: 'CheckCircle',
        color: 'blue',
        agents: [
          { name: 'Evaluator', type: 'Quality Assessment', description: 'Assess output quality with custom metrics' },
          { name: 'Reflection', description: 'Self-improvement through iterative refinement' },
          { name: 'Debate', type: 'Multi-Perspective', description: 'Consider diverse viewpoints for balanced decisions' },
          { name: 'Governor', type: 'Governance', description: 'Enforce policies and validation rules' },
        ]
      },
      {
        title: 'Memory & Learning',
        icon: 'Database',
        color: 'green',
        agents: [
          { name: 'Memory', description: 'Long-term context and knowledge storage' },
          { name: 'Adaptive Memory', description: 'Dynamic prioritization and intelligent recall' },
          { name: 'Curriculum', description: 'Progressive learning with adaptive difficulty' },
          { name: 'Meta Evolver', description: 'Strategy evolution and optimization' },
        ]
      },
      {
        title: 'Coordination & Execution',
        icon: 'Users',
        color: 'purple',
        agents: [
          { name: 'Multi-Agent', description: 'Parallel execution across multiple agents' },
          { name: 'Swarm', description: 'Collective intelligence and consensus building' },
          { name: 'Hierarchical', description: 'Structured delegation and supervision' },
          { name: 'Toolformer', description: 'Dynamic tool selection and API integration' },
        ]
      },
      {
        title: 'Specialized Capabilities',
        icon: 'Zap',
        color: 'orange',
        agents: [
          { name: 'Generative', description: 'Content generation for any domain' },
          { name: 'Voyager', description: 'Exploration and novel solution discovery' },
          { name: 'Auto Loop', description: 'Autonomous self-directed operation' },
        ]
      }
    ],
    ctaText: 'Transform Your Business Operations'
  }
];

export function getUseCase(id: string): UseCase | undefined {
  return USE_CASES.find(uc => uc.id === id);
}

export function getDefaultUseCase(): UseCase {
  return USE_CASES[0]; // compliance as default
}
